# SkinScreen

Requires Python >= 3.10

## Develop and test locally

You can host a website on your local machine which can be accessed in the browser at http://localhost:8000/. This is much easier than developing and testing directly on the Lightsail server, since you can only use the terminal/cli for that.

### Install and Configure AWS CLI for local access to SageMaker

Before your local machine can inference with SageMaker, you will need to install and configure aws-cli by following [this guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html). 

Once aws-cli is installed, run the following and fill in the prompts as described next.

```bash
aws configure
```

You can use the same access key and secret access key from the Wordpress IAM user that we set up.

```
AWS Access Key ID: [get it from the csv on GDrive]
AWS Secret Access Key ID: [get it from the csv on GDrive]
Default Region: us-west-2
Output Format: json
```

### Configure environment and deploy to localhost:8000

Clone this repo and navigate to it in the cli. Install the environment dependencies.  
*NOTE: Python version 3.10 or higher is required.*

```bash 
pip3 install -r requirements.txt
```

Launch the website at localhost:8000 with the following command. 

```bash
uvicorn main:app --reload
```

When you make changes to any of the project files, the server will automatically deploy the new changes to localhost:8000.

It will continue to run in the kernel until terminated or the cli is closed.

Stop it with `Ctrl+c`.

## Deploy with Amazon Lightsail

Once you are ready to deploy changes to the public website, push them to the GitHub repository and follow these steps.

* Log in to the management console through the AWS Organization portal and navigate to Amazon Lightsail. 

* Open the in-browser terminal for the SkinScreen-Ubuntu instance.

* Navigate to the project directory and pull new changes from the git repository.

```bash
cd SkinScreen
git pull
```

The site will update automatically.

### Debugging note: the server runs in the background with tmux

Normally, launching the server with `uvicorn main:app --reload` requires that the terminal is open to continue running, and it will shut down when you close it. So, we use tmux to constantly serve the website in the background. It will stay up while the terminal is closed, and it allows you to use the terminal at the same time without taking the site down.

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


