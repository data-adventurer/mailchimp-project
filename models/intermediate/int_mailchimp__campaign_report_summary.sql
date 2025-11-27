select
    id as campaign_id,
    report_summary:opens::int as opens,
    report_summary:unique_opens::int as unique_opens,
    report_summary:open_rate::float as open_rate,
    report_summary:clicks::int as clicks,
    report_summary:subscriber_clicks::int as subscriber_clicks,
    report_summary:click_rate::float as click_rate
from {{ ref('stg_mailchimp__campaigns') }}
