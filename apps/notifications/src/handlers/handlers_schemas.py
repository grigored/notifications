TYPE = "type"
OBJECT = "object"
NULLABLE_OBJECT = ["object", "null"]
ARRAY = "array"
NULLABLE_ARRAY = ["array", "null"]
ITEMS = "items"
STRING = "string"
REQUIRED = "required"
PROPERTIES = "properties"

schema_email = {
    TYPE: NULLABLE_OBJECT,
    REQUIRED: ["receiver", "subject"],
    PROPERTIES: {
        "sender": {TYPE: STRING},
        "receiver": {
            TYPE: ARRAY,
            ITEMS: {TYPE: STRING},
        },
        "subject": {TYPE: STRING},
        "text": {TYPE: STRING},
        "html": {TYPE: STRING},
        "data": {TYPE: OBJECT},
        "pdfs": {
            TYPE: NULLABLE_ARRAY,
            ITEMS: {
                TYPE: OBJECT,
                REQUIRED: ["body", "filename"],
                PROPERTIES: {
                    "body": {TYPE: STRING},
                    "filename": {TYPE: STRING},
                },
            },
        },
    },
}

schema_sms = {
    TYPE: NULLABLE_OBJECT,
    REQUIRED: ["receiver", "body"],
    PROPERTIES: {
        "sender": {TYPE: STRING},
        "receiver": {TYPE: STRING},
        "body": {TYPE: STRING},
        "data": {TYPE: OBJECT},
    },
}

schema_notification = {
    TYPE: OBJECT,
    PROPERTIES: {
        "email": schema_email,
        "sms": schema_sms,
    },
}
