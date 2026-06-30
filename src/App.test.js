import { render, screen } from '@testing-library/react';
import App from './App';

test('renders learn react link', () => {
  render(<App />);
  const linkElement = screen.getByText(/Actually Build Backend Apps Using AI/i);
  expect(linkElement).toBeInTheDocument();
});
