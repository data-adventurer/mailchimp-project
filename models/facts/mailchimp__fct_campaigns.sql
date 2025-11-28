with stg_mailchimp__campaigns as (

    select * from {{ ref('stg_mailchimp__campaigns') }}
  
),

int_mailchimp__campaign_report_summary as (

    select * from {{ ref('int_mailchimp__campaign_report_summary') }}
  
),

total_emails_sent as (
    select
        id
        ,status
        ,SUM(emails_sent) as emails_sent
    from stg_mailchimp__campaigns
    group by 1,2
),

join_tables_together as (
    select 
        campaign_id
        ,opens
        ,unique_opens
        ,open_rate
        ,clicks
        ,subscriber_clicks
        ,click_rate
        ,emails_sent
        ,status
    from int_mailchimp__campaign_report_summary as crs 
    left join total_emails_sent as tms
    on crs.campaign_id = tms.id
),

mailchimp__fct_campaigns as (
    select 
        *
    from join_tables_together
    where status = 'sent'
)

select * from mailchimp__fct_campaigns