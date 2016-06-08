"""a."""
import commands
import random
from flask import Flask, request, redirect, render_template

app = Flask(__name__)


def remote_addr(request):
    """S."""
    if not request.headers.getlist("X-Forwarded-For"):
        ip = request.remote_addr
    else:
        ip = request.headers.getlist("X-Forwarded-For")[0]
    return ip


def login_info(data, request):
    """S."""
    data['system_time'] = commands.getoutput('date')
    data['remote_ip'] = remote_addr(request)
    return data


def execute_commands(command, args):
    """S."""
    executable = '{0} {1}'.format(command, args)
    return commands.getoutput(executable)


def get_random_command(request):
    """S."""
    commands = []
    bash = {'command': 'uptime', 'args': ''}
    commands.append(bash)
    bash = {'command': 'host', 'args': remote_addr(request)}
    commands.append(bash)
    return random.choice(commands)


def bash_commands(request):
    """S."""
    script = []
    line = {}
    line['command'] = 'cat'
    line['args'] = '.aboutme'
    line['output'] = execute_commands(line['command'], line['args'])
    script.append(line)
    line = get_random_command(request)
    line['output'] = execute_commands(line['command'], line['args'])
    script.append(line)
    return script


@app.route('/')
def index():
    """S."""
    return app.send_static_file('index.html')


@app.route('/data')
def data():
    """S."""
    data = {}
    data['user'] = 'kushagra'
    data['host'] = 'kushagra.net.in'
    data['script'] = bash_commands(request)
    data = login_info(data, request)
    return render_template('data.j2', **data)


@app.errorhandler(404)
def handle_404(e):
    """S."""
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
#    app.run(debug=True)
