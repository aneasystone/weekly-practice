from dotenv import load_dotenv
load_dotenv()

import os
DAYTONA_API_KEY = os.getenv("DAYTONA_API_KEY")

# ------------------------------------------------

from daytona_sdk import Daytona, DaytonaConfig, CreateSandboxParams, CodeRunParams

# Initialize the Daytona client
daytona = Daytona(DaytonaConfig(api_key=DAYTONA_API_KEY))

# Create the Sandbox instance
sandbox = daytona.create(CreateSandboxParams(language="python"))

# Run code securely inside the Sandbox
params = CodeRunParams(
    argv=[
        "-h", "-i"
    ], 
    env={
        'DEMO_ENV': 'xxx'
    }
)
response = sandbox.process.code_run('''
import os
import sys

print("Hello")
print("环境变量：DEMO_ENV = ", os.getenv("DEMO_ENV"))
print("命令行参数：", *[f"{arg}" for _, arg in enumerate(sys.argv)])
''', params=params)
if response.exit_code != 0:
    print(f"Error running code: {response.exit_code} {response.result}")
else:
    print(response.result)

# Clean up the Sandbox
daytona.remove(sandbox)