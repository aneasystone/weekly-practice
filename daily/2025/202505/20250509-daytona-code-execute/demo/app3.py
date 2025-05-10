
from dotenv import load_dotenv
load_dotenv()

import os
DAYTONA_API_KEY = os.getenv("DAYTONA_API_KEY")

# ------------------------------------------------

import time
import asyncio
from daytona_sdk import Daytona, DaytonaConfig, CreateSandboxParams, SessionExecuteRequest

async def main():
    # Initialize the Daytona client
    daytona = Daytona(DaytonaConfig(api_key=DAYTONA_API_KEY))

    # Create the Sandbox instance
    sandbox = daytona.create(CreateSandboxParams(language="python"))

    # Create the session
    session_id = "my-session"
    sandbox.process.create_session(session_id)

    # Execute long-running command securely inside the Sandbox
    req = SessionExecuteRequest(
        run_async=True,
        command="for ((i=0; i<10; i++)); do echo $i; sleep 1; done"
    )
    response = sandbox.process.execute_session_command(session_id, req)

    # Logging
    while(True):
        time.sleep(1)
        command = sandbox.process.get_session_command(session_id, response.cmd_id)
        if command.exit_code is None:
            print(f"Command is running ...")
            continue
        if command.exit_code == 0:
            print(f"Command {command.command} completed successfully")    
        else:
            print(f"Command {command.command} failed")
        logs = sandbox.process.get_session_command_logs(session_id, response.cmd_id)
        print(f"{logs}")
        break

    # Logging
    # await sandbox.process.get_session_command_logs_async(
    #     session_id,
    #     response.cmd_id,
    #     lambda chunk: print(f"Log chunk: {chunk}")
    # )

    # Clean up the Sandbox
    daytona.remove(sandbox)

if __name__ == "__main__":
    asyncio.run(main())