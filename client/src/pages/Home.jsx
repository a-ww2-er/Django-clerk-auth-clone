import React, { useEffect, useState } from "react";
import api from "../api";
import "../styles/notes.css";

function Home() {
  const [notes, setNotes] = useState([]);
  const [content, setContent] = useState("");
  const [title, setTitle] = useState("");
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [selectedNote, setSelectedNote] = useState(null);

  const getNotes = () => {
    api
      .get("/api/notes/")
      .then((res) => res.data)
      .then((data) => setNotes(data))
      .catch((err) => {
        alert(err);
      });
  };

  const deleteNote = (id) => {
    api
      .delete(`/api/notes/delete/${id}/`)
      .then((res) => {
        if (res.status === 204) {
          alert("Note deleted!");
          setSelectedNote(null);
        } else alert("Failed to delete note.");
        getNotes();
      })
      .catch((err) => alert(err));
  };

  const createNote = (e) => {
    e.preventDefault();
    api
      .post("/api/notes/", { content, title })
      .then((res) => {
        if (res.status === 201) {
          alert("Note created!");
          setIsCreateModalOpen(false);
          setTitle("");
          setContent("");
        } else alert("Failed to create note.");
        getNotes();
      })
      .catch((err) => alert(err));
  };

  useEffect(() => {
    getNotes();
  }, []);

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  };

  return (
    <div className="notes-container">
      <header className="notes-header">
        <h1>My Notes</h1>
        <button
          className="create-note-button"
          onClick={() => setIsCreateModalOpen(true)}
        >
          + New Note
        </button>
      </header>

      <div className="notes-grid">
        {notes.map((note) => (
          <div
            key={note.id}
            className="note-card"
            onClick={() => setSelectedNote(note)}
          >
            <h3 className="note-title">{note.title}</h3>
            <p className="note-preview">
              {note.content.length > 100
                ? `${note.content.substring(0, 100)}...`
                : note.content}
            </p>
            <div className="note-date">{formatDate(note.created_at)}</div>
          </div>
        ))}
      </div>

      {/* Create Note Modal */}
      {isCreateModalOpen && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h2>Create New Note</h2>
              <button
                className="close-button"
                onClick={() => setIsCreateModalOpen(false)}
              >
                ×
              </button>
            </div>
            <form onSubmit={createNote} className="note-form">
              <div className="form-group">
                <label htmlFor="title">Title</label>
                <input
                  id="title"
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="Enter note title"
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="content">Content</label>
                <textarea
                  id="content"
                  value={content}
                  onChange={(e) => setContent(e.target.value)}
                  placeholder="Enter note content"
                  required
                />
              </div>
              <button type="submit" className="submit-button">
                Create Note
              </button>
            </form>
          </div>
        </div>
      )}

      {/* View/Delete Note Modal */}
      {selectedNote && (
        <div className="modal-overlay">
          <div className="modal-content view-note-modal">
            <div className="modal-header">
              <h2>{selectedNote.title}</h2>
              <button
                className="close-button"
                onClick={() => setSelectedNote(null)}
              >
                ×
              </button>
            </div>
            <div className="note-full-content">
              <p>{selectedNote.content}</p>
              <div className="note-metadata">
                <span>Created: {formatDate(selectedNote.created_at)}</span>
              </div>
            </div>
            <div className="modal-footer">
              <button
                className="delete-button"
                onClick={() => deleteNote(selectedNote.id)}
              >
                Delete Note
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Home;
