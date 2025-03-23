const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

export async function registerUser(userData) {
  const response = await fetch(`${API_BASE_URL}/users/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(userData),
  });
  return response.json();
}

export async function loginUser(username, password) {
  const data = new URLSearchParams();
  data.append("username", username);
  data.append("password", password);

  const response = await fetch(`${API_BASE_URL}/users/token`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: data.toString(),
  });
  return response.json();
}

export async function getUserData(token) {
  if (!token) {
    console.error("No access token found");
    return null;
  }
  const response = await fetch(`${API_BASE_URL}/users/me`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`,
    },
  });
  if (!response.ok) {
    console.error("Failed to fetch user data:", response.status);
    return null;
  }
  return response.json();
}

export async function getTickets(filters = {}) {
  const token = localStorage.getItem("access_token");
  const queryParams = new URLSearchParams(filters).toString();
  const response = await fetch(`${API_BASE_URL}/tickets/view?${queryParams}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`,
    },
  });
  return response.json();
}

export async function createTicket(ticketData) {
  const token = localStorage.getItem("access_token");
  const response = await fetch(`${API_BASE_URL}/tickets/create`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`,
    },
    body: JSON.stringify(ticketData),
  });
  return response.json();
}

export async function updateTicketStatus(ticketId, status) {
  const token = localStorage.getItem("access_token");
  const response = await fetch(`${API_BASE_URL}/tickets/${ticketId}/status`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`,
    },
    body: JSON.stringify({ status }),
  });
  return response.json();
}

export async function assignTicket(ticketId, assignedToId) {
  const token = localStorage.getItem("access_token");
  const response = await fetch(`${API_BASE_URL}/tickets/${ticketId}/assign`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`,
    },
    body: JSON.stringify({ assigned_to_id: assignedToId }),
  });
  return response.json();
}

export async function getSupportMembers() {
  const token = localStorage.getItem("access_token");
  const response = await fetch(`${API_BASE_URL}/users/support_members`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`,
    },
  });
  return response.json();
}
