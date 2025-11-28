with int_mailchimp__campaign_recipients as (

    select * from {{ ref('int_mailchimp__campaign_recipients') }}
  
),

mailchimp__dim_camapigns as (

    select * from {{ ref('mailchimp__dim_camapigns') }}
  
),

mailchimp__fct_campaigns as (

    select * from {{ ref('mailchimp__fct_campaigns') }}
  
),
mart_mailchimp__campaigns as (
    select 
        cr.campaign_id
        ,SUM(recipient_count) as recipient_count
        ,SUM(unique_opens) as unique_opens
    from mailchimp__dim_camapigns as dc
    join int_mailchimp__campaign_recipients as cr 
    on dc.campaign_id = cr.campaign_id
    join mailchimp__fct_campaigns as fc 
    on dc.campaign_id = fc.campaign_id
    where title is not null
    group by 1
    order by recipient_count desc, unique_opens desc
)

select * from mart_mailchimp__campaigns