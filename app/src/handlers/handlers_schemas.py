TYPE = "type"
OBJECT = "object"
NULLABLE_OBJECT = ["object", "null"]
ARRAY = "array"
NULLABLE_ARRAY = ["array", "null"]
ITEMS = "items"
STRING = "string"
REQUIRED = "required"
PROPERTIES = "properties"

schema_notification = {
    TYPE: OBJECT,
    PROPERTIES: {
        "email": {
            TYPE: NULLABLE_OBJECT,
            REQUIRED: ["receiver", "email_subject_template"],
            PROPERTIES: {
                "sender": {TYPE: STRING},
                "receiver": {TYPE: STRING},
                "email_subject_template": {TYPE: STRING},
                "email_text_template": {TYPE: STRING},
                "email_html_template": {TYPE: STRING},
                "data": {TYPE: OBJECT},
                "pdfs": {
                    TYPE: NULLABLE_ARRAY,
                    ITEMS: {
                        TYPE: OBJECT,
                        REQUIRED: ["template", "filename"],
                        PROPERTIES: {
                            "template": {TYPE: STRING},
                            "filename": {TYPE: STRING},
                        },
                    },
                },
            },
        },
        "sms": {
            TYPE: NULLABLE_OBJECT,
        },
    },
}
