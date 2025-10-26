import uvloop
import asyncio
import os
import sys

# Install uvloop as the default event loop
uvloop.install()

# Run the main module
if __name__ == '__main__':
    os.environ['PYTHONPATH'] = '/app'
    sys.path.insert(0, '/app')
    from src.nodes.base_node import main
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass