import consul
import socket
import logging
import os
import random

logger = logging.getLogger(__name__)

def get_ip_address():
    """Get the local IP address of the machine"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def register_service(service_name, service_port, service_id=None, service_address=None, tags=None):
    """
    Register a service with Consul
    """
    consul_host = os.getenv('CONSUL_HOST', 'localhost')
    consul_port = int(os.getenv('CONSUL_PORT', 8500))
    
    if not service_address:
        service_address = get_ip_address()
        
    if not service_id:
        service_id = f"{service_name}-{service_address}-{service_port}"
        
    if not tags:
        tags = []

    try:
        c = consul.Consul(host=consul_host, port=consul_port)
        
        # Check endpoint
        check_http = f"http://{service_address}:{service_port}/health/"
        
        c.agent.service.register(
            service_name,
            service_id=service_id,
            address=service_address,
            port=service_port,
            tags=tags,
            check=consul.Check.http(check_http, interval="10s", timeout="5s", deregister="1m")
        )
        logger.info(f"Successfully registered service {service_name} with ID {service_id}")
        return True, service_id
    except Exception as e:
        logger.error(f"Failed to register service {service_name}: {e}")
        return False, None

def deregister_service(service_id):
    """
    Deregister a service from Consul
    """
    consul_host = os.getenv('CONSUL_HOST', 'localhost')
    consul_port = int(os.getenv('CONSUL_PORT', 8500))
    
    try:
        c = consul.Consul(host=consul_host, port=consul_port)
        c.agent.service.deregister(service_id)
        logger.info(f"Successfully deregistered service ID {service_id}")
        return True
    except Exception as e:
        logger.error(f"Failed to deregister service ID {service_id}: {e}")
        return False

def get_service(service_name):
    """
    Discover a service from Consul
    Returns the base URL of a healthy service instance
    """
    consul_host = os.getenv('CONSUL_HOST', 'localhost')
    consul_port = int(os.getenv('CONSUL_PORT', 8500))
    
    try:
        c = consul.Consul(host=consul_host, port=consul_port)
        index, services = c.health.service(service_name, passing=True)
        
        if not services:
            logger.warning(f"No healthy instances found for service: {service_name}")
            return None
            
        # Basic load balancing: random selection
        service = random.choice(services)
        service_addr = service['Service']['Address']
        service_port = service['Service']['Port']
        
        return f"http://{service_addr}:{service_port}"
        
    except Exception as e:
        logger.error(f"Failed to discover service {service_name}: {e}")
        return None
