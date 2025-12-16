import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import path from "path";
import { componentTagger } from "lovable-tagger";
import Consul from "consul";
import { v4 as uuidv4 } from "uuid";
import os from "os";

// Get dynamic IP address (similar to backend's get_ip_address)
function getIpAddress(): string {
  const interfaces = os.networkInterfaces();

  // Try to find a non-internal IPv4 address
  for (const name of Object.keys(interfaces)) {
    const iface = interfaces[name];
    if (!iface) continue;

    for (const addr of iface) {
      // Skip internal (loopback) and IPv6 addresses
      if (addr.family === 'IPv4' && !addr.internal) {
        return addr.address;
      }
    }
  }

  // Fallback to localhost if no external IP found
  return '127.0.0.1';
}

// Consul configuration
const CONSUL_HOST = process.env.CONSUL_HOST || "localhost";
const CONSUL_PORT = parseInt(process.env.CONSUL_PORT || "8500");
const SERVICE_NAME = "frontend-service";
const SERVICE_PORT = 8080;
const SERVICE_IP = process.env.SERVICE_IP || getIpAddress();

let serviceId: string | null = null;
let consulClient: Consul.Consul | null = null;

// Get service URL from Consul
async function getServiceUrl(serviceName: string): Promise<string | null> {
  try {
    const consul = new Consul({ host: CONSUL_HOST, port: CONSUL_PORT });
    const result = await consul.health.service({ service: serviceName, passing: true });

    if (result && result.length > 0) {
      const service = result[0];
      const address = service.Service.Address;
      const port = service.Service.Port;
      return `http://${address}:${port}`;
    }

    console.warn(`No healthy instances found for service: ${serviceName}`);
    return null;
  } catch (error) {
    console.error(`Failed to discover service ${serviceName}:`, error);
    return null;
  }
}

// Register service with Consul
async function registerService() {
  try {
    consulClient = new Consul({ host: CONSUL_HOST, port: CONSUL_PORT });
    serviceId = `${SERVICE_NAME}-${SERVICE_IP}-${SERVICE_PORT}-${uuidv4()}`;

    await consulClient.agent.service.register({
      id: serviceId,
      name: SERVICE_NAME,
      address: SERVICE_IP,
      port: SERVICE_PORT,
      tags: ["frontend", "vite", "react"],
      check: {
        http: `http://${SERVICE_IP}:${SERVICE_PORT}/`,
        interval: "10s",
        timeout: "5s",
        deregistercriticalserviceafter: "1m",
      },
    });

    console.log(`✅ Registered ${SERVICE_NAME} with Consul (ID: ${serviceId})`);
  } catch (error) {
    console.error("❌ Failed to register with Consul:", error);
  }
}

// Deregister service from Consul
async function deregisterService() {
  if (consulClient && serviceId) {
    try {
      await consulClient.agent.service.deregister(serviceId);
      console.log(`✅ Deregistered ${SERVICE_NAME} from Consul`);
    } catch (error) {
      console.error("❌ Failed to deregister from Consul:", error);
    }
  }
}

// Setup graceful shutdown
function setupShutdownHandlers() {
  const shutdown = async () => {
    await deregisterService();
    process.exit(0);
  };

  process.on("SIGINT", shutdown);
  process.on("SIGTERM", shutdown);
  process.on("exit", () => {
    if (serviceId) {
      console.log("Cleaning up...");
    }
  });
}

// https://vitejs.dev/config/
export default defineConfig(async ({ mode }) => {
  // Register with Consul in development mode
  if (mode === "development") {
    await registerService();
    setupShutdownHandlers();
  }

  // Discover backend services
  const userServiceUrl = await getServiceUrl("user-service") || process.env.USER_SERVICE_URL || "http://localhost:8001";
  const booksServiceUrl = await getServiceUrl("book-service") || process.env.BOOK_SERVICE_URL || "http://localhost:8002";
  const loansServiceUrl = await getServiceUrl("loans-service") || process.env.LOANS_SERVICE_URL || "http://localhost:8003";
  const notificationsServiceUrl = await getServiceUrl("notification-service") || process.env.NOTIFICATIONS_SERVICE_URL || "http://localhost:8004";

  console.log("🔍 Discovered services:");
  console.log(`  User Service: ${userServiceUrl}`);
  console.log(`  Books Service: ${booksServiceUrl}`);
  console.log(`  Loans Service: ${loansServiceUrl}`);
  console.log(`  Notifications Service: ${notificationsServiceUrl}`);

  return {
    server: {
      host: "::",
      port: SERVICE_PORT,
      proxy: {
        "/api/users": {
          target: userServiceUrl,
          changeOrigin: true,
          secure: false,
        },
        "/api/books": {
          target: booksServiceUrl,
          changeOrigin: true,
          secure: false,
        },
        "/api/loans": {
          target: loansServiceUrl,
          changeOrigin: true,
          secure: false,
        },
        "/api/notifications": {
          target: notificationsServiceUrl,
          changeOrigin: true,
          secure: false,
        },
      },
    },
    plugins: [react(), mode === "development" && componentTagger()].filter(Boolean),
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "./src"),
      },
    },
  };
});
