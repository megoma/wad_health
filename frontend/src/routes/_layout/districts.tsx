import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/_layout/districts')({
  component: () => <div>Hello /_layout/districts!</div>
})