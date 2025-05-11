from dotenv import load_dotenv
load_dotenv()

import os
DAYTONA_API_KEY = os.getenv("DAYTONA_API_KEY")

# ------------------------------------------------

from daytona_sdk import Daytona, DaytonaConfig, CreateSandboxParams, CodeRunParams, SandboxResources

# Initialize the Daytona client
daytona = Daytona(DaytonaConfig(api_key=DAYTONA_API_KEY))

# Create the Sandbox instance
params = CreateSandboxParams(
    language="python",
    image="debian:12.9",
    env_vars={"DEBUG": "true"},
    resources=SandboxResources(cpu=2, memory=4),
    auto_stop_interval=0
)
sandbox = daytona.create(params)

# Run code securely inside the Sandbox
response = sandbox.process.exec("echo $DEBUG")
if response.exit_code != 0:
    print(f"Error running code: {response.exit_code} {response.result}")
else:
    print(response.result)

# Clean up the Sandbox
daytona.remove(sandbox)