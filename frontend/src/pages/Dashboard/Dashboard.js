import React, { useContext, useEffect, useState } from "react";
import { AuthContext } from "../../contexts/AuthContext";
import { useNavigate } from "react-router-dom";
import {
  getTickets,
  createTicket,
  updateTicketStatus,
  assignTicket,
  getSupportMembers
} from "../../services/api";
import styles from "./Dashboard.module.css";

function Dashboard() {
  const { user, logout } = useContext(AuthContext);
  const [tickets, setTickets] = useState([]);
  const [supportMembers, setSupportMembers] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    if (user) {
      let filters = {};
      if (user.role_id === 1) {
        filters = { user_id: user.id.toString() };
      } else if (user.role_id === 2) {
        filters = { assigned_to: user.id.toString() };
      }
      getTickets(filters).then(setTickets);
    }
  }, [user]);

  useEffect(() => {
    if (user && user.role_id === 3) {
      getSupportMembers().then(setSupportMembers);
    }
  }, [user]);

  const handleCreateTicket = async () => {
    if (!title.trim()) {
      alert("Title is required!");
      return;
    }
    const ticketData = { title, description };
    try {
      await createTicket(ticketData);
      setShowModal(false);
      setTitle("");
      setDescription("");
      let filters = {};
      if (user.role_id === 1) {
        filters = { user_id: user.id.toString() };
      } else if (user.role_id === 2) {
        filters = { assigned_to: user.id.toString() };
      } else if (user.role_id === 3) {
        filters = {};
      }
      getTickets(filters).then(setTickets);
    } catch (error) {
      console.error("Error creating ticket:", error);
      alert("Failed to create ticket. Please try again.");
    }
  };

  const handleStatusChange = async (ticketId, newStatus) => {
    try {
      await updateTicketStatus(ticketId, newStatus);
      let filters = {};
      if (user.role_id === 2) {
        filters = { assigned_to: user.id.toString() };
      } else if (user.role_id === 3) {
        filters = {};
      }
      getTickets(filters).then(setTickets);
    } catch (error) {
      console.error("Error updating ticket status:", error);
      alert("Failed to update ticket status.");
    }
  };

  const handleAssignChange = async (ticketId, assignedToId) => {
    try {
      await assignTicket(ticketId, assignedToId);
      getTickets({}).then(setTickets);
    } catch (error) {
      console.error("Error assigning ticket:", error);
      alert("Failed to assign ticket.");
    }
  };

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  const closeModal = (e) => {
    if (e.target.classList.contains(styles.modalOverlay)) {
      setShowModal(false);
    }
  };

  if (!user) {
    return <div>Loading...</div>;
  }

  return (
    <div className={styles.dashboardContainer}>
      {/* Fixed Header */}
      <div className={styles.header}>
        <h2>Dashboard</h2>
        <div className={styles.headerButtons}>
          {user.role_id === 1 && (
            <button className={styles.createButton} onClick={() => setShowModal(true)}>
              Create Ticket
            </button>
          )}
          <button className={styles.logoutButton} onClick={handleLogout}>
            Log Out
          </button>
        </div>
      </div>

      {/* Scrollable Ticket List */}
      <div className={styles.ticketListContainer}>
        {user.role_id === 1 && (
          <>
            <h3>Your Tickets</h3>
            <ul className={styles.ticketList}>
              {tickets.length > 0 ? (
                tickets.map((ticket) => (
                  <li key={ticket.id} className={styles.ticketItem}>
                    <strong>{ticket.title}</strong>
                    <p>{ticket.description}</p>
                    <span>Status: {ticket.status}</span>
                  </li>
                ))
              ) : (
                <p>No tickets found.</p>
              )}
            </ul>
          </>
        )}

        {user.role_id === 2 && (
          <>
            <h3>Assigned Tickets</h3>
            <ul className={styles.ticketList}>
              {tickets.length > 0 ? (
                tickets.map((ticket) => (
                  <li key={ticket.id} className={styles.ticketItem}>
                    <strong>{ticket.title}</strong>
                    <p>{ticket.description}</p>
                    <span>Status: {ticket.status}</span>
                    <div className={styles.buttonGroup}>
                      <button onClick={() => handleStatusChange(ticket.id, "in_progress")}>Start</button>
                      <button onClick={() => handleStatusChange(ticket.id, "resolved")}>Resolve</button>
                    </div>
                  </li>
                ))
              ) : (
                <p>No assigned tickets found.</p>
              )}
            </ul>
          </>
        )}

        {user.role_id === 3 && (
          <>
            <h3>All Tickets</h3>
            <ul className={styles.ticketList}>
              {tickets.length > 0 ? (
                tickets.map((ticket) => (
                  <li key={ticket.id} className={styles.ticketItem}>
                    <strong>{ticket.title}</strong>
                    <p>{ticket.description}</p>
                    <span>Status: {ticket.status}</span>
                    <div className={styles.assignContainer}>
                      <label htmlFor={`assign-${ticket.id}`}>Assign:</label>
                      <select
                        id={`assign-${ticket.id}`}
                        defaultValue=""
                        onChange={(e) => {
                          const value = e.target.value;
                          if (value !== "") {
                            handleAssignChange(ticket.id, value);
                          }
                        }}
                      >
                        <option value="" disabled>
                          Select Support Member
                        </option>
                        <option value={user.id}>Assign to me</option>
                        {supportMembers.map((member) => (
                          <option key={member.id} value={member.id}>
                            {member.username}
                          </option>
                        ))}
                      </select>
                    </div>
                  </li>
                ))
              ) : (
                <p>No tickets found.</p>
              )}
            </ul>
          </>
        )}
      </div>

      {/* Pop-up Form for Creating Ticket */}
      {showModal && (
        <div className={styles.modalOverlay} onClick={closeModal}>
          <div className={styles.modal}>
            <button className={styles.closeButton} onClick={() => setShowModal(false)}>
              ×
            </button>
            <h3>Create Ticket</h3>
            <label>Title:</label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
            />
            <label>Description:</label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
            <div className={styles.buttonGroup}>
              <button onClick={handleCreateTicket}>Submit</button>
              <button onClick={() => setShowModal(false)}>Cancel</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Dashboard;
