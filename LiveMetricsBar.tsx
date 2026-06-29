@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 98%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 221.2 83.2% 53.3%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 221.2 83.2% 53.3%;
    --radius: 0.5rem;
    --sidebar-width: 220px;
    --inspector-width: 320px;
    --topbar-height: 52px;
    --timeline-height: 80px;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --card: 222.2 84% 7%;
    --card-foreground: 210 40% 98%;
    --popover: 222.2 84% 4.9%;
    --popover-foreground: 210 40% 98%;
    --primary: 217.2 91.2% 59.8%;
    --primary-foreground: 222.2 47.4% 11.2%;
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 224.3 76.3% 48%;
  }

  * {
    @apply border-border;
  }

  html {
    font-feature-settings: 'cv02', 'cv03', 'cv04', 'cv11';
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-rendering: optimizeLegibility;
  }

  body {
    @apply bg-background text-primary-text font-sans;
  }

  /* Custom scrollbar */
  ::-webkit-scrollbar {
    width: 5px;
    height: 5px;
  }

  ::-webkit-scrollbar-track {
    background: transparent;
  }

  ::-webkit-scrollbar-thumb {
    background: #D1D5DB;
    border-radius: 100px;
  }

  ::-webkit-scrollbar-thumb:hover {
    background: #9CA3AF;
  }
}

@layer components {
  /* React Flow overrides */
  .react-flow__node {
    @apply cursor-pointer;
  }

  .react-flow__edge-path {
    stroke-width: 1.5;
  }

  .react-flow__controls {
    @apply shadow-none border border-border rounded-lg overflow-hidden;
  }

  .react-flow__controls-button {
    @apply border-border bg-white hover:bg-gray-50 transition-colors;
  }

  .react-flow__minimap {
    @apply border border-border rounded-lg overflow-hidden;
  }

  /* Packet animation */
  .packet {
    animation: travelPacket 1.5s ease-in-out infinite;
  }

  @keyframes travelPacket {
    0% { offset-distance: 0%; opacity: 0; }
    10% { opacity: 1; }
    90% { opacity: 1; }
    100% { offset-distance: 100%; opacity: 0; }
  }

  /* Status indicators */
  .status-online {
    @apply text-green-600 bg-green-50;
  }

  .status-warning {
    @apply text-orange-600 bg-orange-50;
  }

  .status-error {
    @apply text-red-600 bg-red-50;
  }

  .status-offline {
    @apply text-gray-500 bg-gray-100;
  }

  /* Log entries */
  .log-info {
    @apply text-blue-600;
  }

  .log-warning {
    @apply text-orange-600;
  }

  .log-error {
    @apply text-red-600;
  }

  .log-debug {
    @apply text-gray-500;
  }

  /* Metric cards */
  .metric-up {
    @apply text-red-600;
  }

  .metric-down {
    @apply text-green-600;
  }

  .metric-neutral {
    @apply text-secondary-text;
  }

  /* Timeline */
  .timeline-handle {
    @apply bg-blue cursor-col-resize;
  }
}

@layer utilities {
  .font-tabular-nums {
    font-variant-numeric: tabular-nums;
    font-feature-settings: 'tnum';
  }
}
