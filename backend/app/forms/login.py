from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from app.models.users import User

class LoginForm(FlaskForm):
    """登录表单"""
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired(), Length(min=6)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')
    
    def validate_email(self, field):
        """验证邮箱是否存在"""
        user = User.query.filter_by(email=field.data).first()
        if not user:
            raise ValidationError('该邮箱未注册')
