from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class TextSummary(models.Model):
    id = fields.IntField(pk=True)
    url = fields.TextField()
    summary = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.url


# generate a pydantic model from tortoise model
SummarySchema = pydantic_model_creator(TextSummary)
