import { Client } from '@stomp/stompjs';

// Get RabbitMQ WebSocket URL from environment or use dynamic detection
// In browser, we can't query Consul directly, so we rely on:
// 1. Environment variable (set at build time)
// 2. Vite proxy (for development)
// 3. Runtime configuration endpoint (future enhancement)
const getRabbitMQWebSocketURL = () => {
    // Try environment variable first (injected by Vite)
    const envURL = import.meta.env.VITE_RABBITMQ_WS_URL;
    if (envURL) {
        return envURL;
    }

    // Fallback: construct from window.location (assumes RabbitMQ on same host)
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.hostname;
    const port = 15674; // RabbitMQ Web STOMP default port
    return `${protocol}//${host}:${port}/ws`;
};

const RABBITMQ_CONFIG = {
    brokerURL: getRabbitMQWebSocketURL(),
    connectHeaders: {
        login: import.meta.env.VITE_RABBITMQ_USER || 'guest',
        passcode: import.meta.env.VITE_RABBITMQ_PASSWORD || 'guest',
    },
    // debug: function (str: string) {
    //     console.log('STOMP: ' + str);
    // },
    reconnectDelay: 5000,
    heartbeatIncoming: 4000,
    heartbeatOutgoing: 4000,
};

class RabbitMQService {
    private client: Client;
    private connected: boolean = false;

    constructor() {
        this.client = new Client(RABBITMQ_CONFIG);

        this.client.onConnect = (frame) => {
            this.connected = true;
            console.log('RabbitMQ Connected: ' + frame);
        };

        this.client.onStompError = (frame) => {
            console.error('Broker reported error: ' + frame.headers['message']);
            console.error('Additional details: ' + frame.body);
        };

        this.client.activate();
    }

    public publish(destination: string, body: any) {
        if (!this.client.active) {
            console.warn('RabbitMQ client not active, attempting to activate...');
            this.client.activate();
        }

        // Publish to a topic exchange
        // destination should be like '/exchange/library_events/user.create.request'
        // or if using default exchange: '/queue/queue_name'
        // We are using the topic exchange 'library_events' established in backend

        this.client.publish({
            destination: destination,
            body: JSON.stringify(body),
        });
        console.log(`Published message to ${destination}`, body);
    }

    public sendToExchange(routingKey: string, body: any) {
        // STOMP format for topic exchange: /exchange/<exchange_name>/<routing_key>
        // Backend uses 'library_events' topic exchange
        const destination = `/exchange/library_events/${routingKey}`;
        this.publish(destination, body);
    }
}

export const rabbitMQService = new RabbitMQService();
