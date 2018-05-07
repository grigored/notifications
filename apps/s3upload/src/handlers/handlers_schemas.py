TYPE = "type"
OBJECT = "object"
NUMBER = "number"
NULLABLE_OBJECT = ["object", "null"]
ARRAY = "array"
NULLABLE_ARRAY = ["array", "null"]
ITEMS = "items"
STRING = "string"
BOOLEAN = "boolean"
REQUIRED = "required"
PROPERTIES = "properties"

schema_get_data = {
    TYPE: OBJECT,
    REQUIRED: ["filename"],
    PROPERTIES: {
        "filename": {TYPE: STRING},
        "public": {TYPE: BOOLEAN},
        "maxFileSize": {TYPE: NUMBER},
        "postExpire": {TYPE: NUMBER},
        "bucket": {TYPE: STRING},
        "bucketRegion": {TYPE: STRING},
    },
}
