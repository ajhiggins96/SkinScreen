# SkinScreen

## Develop and test locally

Start by installing the requirements.

```bash 
pip3 install -r requirements.txt
```

Then, you can launch the website at localhost:8000 with the following command.

```bash
uvicorn main:app --reload
```

When you make changes to any of the project files, the server will automatically deploy the new changes.

Before your local machine can inference with SageMaker, you will need to install and configure aws-cli by following [this guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html). Be sure to set the default region to us-west-2 in your `~/.aws/config` file.

```
[default]
region=us-west-2
...
```

## Deploy with Amazon Lightsail

Log in to the management console through the AWS Organization portal and navigate to Amazon Lightsail. 

Open the in-browser terminal for the SkinScreen-Ubuntu instance.

Navigate to the project directory and pull new changes from the git repository.

```bash
cd SkinScreen
git pull
```

The site will update automatically.

### The server runs in the background with tmux

Normally, launching the server with `uvicorn main:app --reload` requires that the terminal is open to continue running, and it will shut down when you close it. So, we use tmux to constantly serve the website in the background. It will stay up while the terminal is closed, and it allows you to use the terminal at the same time without interrupting the uvicorn process.

Read [this StackOverflow answer](https://stackoverflow.com/a/42505000) for an intro to tmux.

List active sessions with:

```bash
tmux list-sessions
```

The server should be running in the tmux session called `uvicorn`. Attach to view server logs and stop/start the  server.

```bash
tmux attach-session -t uvicorn
```

To leave a tmux session and return to the original kernel, detach with `Ctrl+B`, then `D`.


