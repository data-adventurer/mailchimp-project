select
    id as campaign_id,
    settings:subject_line::string as subject_line,
    settings:title::string as title,
    settings:from_name::string as from_name,
    settings:reply_to::string as reply_to,
    settings:use_conversation::boolean as use_conversation,
    settings:to_name::string as to_name,
    settings:folder_id::string as folder_id,
    settings:authenticate::boolean as authenticate
from {{ ref('stg_mailchimp__campaigns') }}