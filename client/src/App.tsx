import { SharedStateProvider } from './core/Store';
import Router from "./core/Router"

export default function App() {
  return (
    <SharedStateProvider>
      <Router></Router>
    </SharedStateProvider>
  );
}