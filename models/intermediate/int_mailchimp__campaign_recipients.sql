select
    id as campaign_id,
    recipients:list_id::string as list_id,
    recipients:segment_text::string as segment_text,
    recipients:recipient_count::int as recipient_count
from {{ ref('stg_mailchimp__campaigns') }}
