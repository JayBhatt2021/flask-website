/**
 * index.js
 *
 * Contains the entire JS functionality for this project.
 */

/**
 * Sends a POST request containing noteId to /delete-note
 * and refreshes the page afterward
 *
 * @param  {String} noteId The ID of the note
 */
const deleteNote = noteId => {
    fetch("/delete-note", {
        method: "POST",
        body: JSON.stringify({ noteId: noteId })
    }).then(_res => {
        window.location.href = "/";
    });
}
