# Frontend - Instagram Reel Processor UI

Vue 3 TypeScript frontend for the Instagram Reel Processor.

## Features

- ✅ View all processing tasks
- ✅ Add new tasks with Instagram Reel URLs
- ✅ Real-time status updates (auto-refresh every 5s)
- ✅ Cancel pending/processing tasks
- ✅ View transcripts with language and topics
- ✅ Copy transcript to clipboard
- ✅ Responsive design

## Development

```bash
# Install dependencies
pnpm install

# Run development server
pnpm dev

# Build for production
pnpm build

# Preview production build
pnpm preview
```

## Testing

```bash
# Run unit tests
pnpm test
```

## Configuration

Backend API URL is configured in `src/services/api.ts`:

```typescript
const API_BASE_URL = 'http://localhost:8000/api'
```

For production, update this to your deployed backend URL.
