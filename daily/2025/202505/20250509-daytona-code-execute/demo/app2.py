from dotenv import load_dotenv
load_dotenv()

import os
DAYTONA_API_KEY = os.getenv("DAYTONA_API_KEY")

# ------------------------------------------------

from daytona_sdk import Daytona, DaytonaConfig, CreateSandboxParams

# Initialize the Daytona client
daytona = Daytona(DaytonaConfig(api_key=DAYTONA_API_KEY))

# Create the Sandbox instance
sandbox = daytona.create(CreateSandboxParams(language="python"))

# Execute command securely inside the Sandbox
response = sandbox.process.exec('echo "Hello"')
if response.exit_code != 0:
    print(f"Error running code: {response.exit_code} {response.result}")
else:
    print(response.result)

response = sandbox.process.exec('ls', cwd="/")
if response.exit_code != 0:
    print(f"Error running code: {response.exit_code} {response.result}")
else:
    print(response.result)

response = sandbox.process.exec('echo $DEMO_ENV', env={"DEMO_ENV": "xxx"})
if response.exit_code != 0:
    print(f"Error running code: {response.exit_code} {response.result}")
else:
    print(response.result)

# Clean up the Sandbox
daytona.remove(sandbox)