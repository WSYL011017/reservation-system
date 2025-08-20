import os
from app import create_app, db
from app.models.users import User
from app.models.reservations import Reservation

app = create_app(os.getenv('FLASK_CONFIG', 'default'))

@app.shell_context_processor
def make_shell_context():
    """配置Flask shell上下文"""
    return {'db': db, 'User': User, 'Reservation': Reservation}

@app.cli.command()
def test():
    """运行测试"""
    import pytest
    pytest.main(['-v', 'tests/'])

@app.cli.command()
def cov():
    """运行测试并生成覆盖率报告"""
    import pytest
    pytest.main(['--cov=app', 'tests/'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
