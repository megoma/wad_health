import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/_layout/churches')({
  component: () => <div>Hello /_layout/churches!</div>
})