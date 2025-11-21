// web-frontend/src/api.js
import axios from "axios";
const API_BASE = "http://127.0.0.1:8000/api";

export function uploadCSV(file, username, password) {
  const form = new FormData();
  form.append("file", file);
  return axios.post(`${API_BASE}/upload-csv/`, form, {
    auth: { username, password },
    headers: { "Content-Type": "multipart/form-data" },
  });
}

export function getHistory(username, password) {
  return axios.get(`${API_BASE}/history/`, { auth: { username, password } });
}

export function getPDF(id, username, password) {
  return axios.get(`${API_BASE}/report/${id}/`, {
    auth: { username, password },
    responseType: "blob",
  });
}
