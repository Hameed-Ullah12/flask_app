from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed

class ProductForm(FlaskForm):

    title = StringField(
        "Product Title",
        validators=[DataRequired()]
    )

    description = TextAreaField(
        "Description",
        validators=[DataRequired()]
    )

    quantity = IntegerField(
        "Quantity",
        validators=[DataRequired()]
    )

    image = FileField(
        "Product Image",
        validators=[
            FileAllowed(["jpg", "jpeg", "png"], "Images only!")])

    submit = SubmitField("Save Product")
