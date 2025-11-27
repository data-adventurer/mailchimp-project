with stg_mailchimp__campaigns as (

    select * from {{ ref('stg_mailchimp__campaigns') }}
  
),
int_mailchimp__campaign_tracking as (
    select

        id as campaign_id,
        tracking:opens::boolean as opens,
        tracking:html_clicks::boolean as html_clicks,
        tracking:text_clicks::boolean as text_clicks,
        tracking:goal_tracking::boolean as goal_tracking,
        tracking:google_analytics::string as google_analytics,
        tracking:clicktale::string as clicktale

    from stg_mailchimp__campaigns

)

select * from int_mailchimp__campaign_tracking