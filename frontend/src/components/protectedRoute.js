
/**
 * source: ChatGPT (OpenAI)
 * prompt: "i have a django backend react frontend. i know how to force
 *          users to login on the backend, but idk how to do it in react"
 *          "it's react in javascript not typescript. update the react examples"
 * date: October 15, 2024
 */

import { Navigate, useLocation } from 'react-router-dom';

export default function ProtectedRoute({ children }) {
  const location = useLocation();

  const token = localStorage.getItem('authToken');

  if (!!!token) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
};
