from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField, IntegerField
from wtforms.validators import DataRequired, NumberRange, InputRequired
from wtforms import ValidationError

ALLOWED_EXTENSIONS = set(['png', 'jpg'])


# 用于判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


class PictureForm(FlaskForm):
    pic = FileField('pic', validators=[DataRequired(), ])
    Top_b = IntegerField('top of Subgraph', validators=[DataRequired(), NumberRange(0, 100), ], default=10)
    Bottom_b = IntegerField('bottom of Subgraph', validators=[DataRequired(), NumberRange(0, 100), ], default=30)
    # DateRequired 不能是0或空字符串
    Left_b = IntegerField('Left of Subgraph', validators=[InputRequired(), NumberRange(0, 100), ], default=0)
    Right_b = IntegerField('Right of Subgraph', validators=[InputRequired(), NumberRange(0, 100), ], default=0)
    submit = SubmitField('Submit')

    def validate_pic(self, field):
        if not allowed_file(filename=field.data.filename):
            raise ValidationError('FileType is not .jpg or .png !')

