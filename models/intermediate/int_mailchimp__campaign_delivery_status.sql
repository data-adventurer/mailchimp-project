with stg_mailchimp__campaigns as (

    select * from {{ ref('stg_mailchimp__campaigns') }}
  
),
 int_mailchimp__campaign_delivery_status as (
    select
        id as campaign_id
        ,delivery_status:enabled::boolean as enabled
        ,delivery_status:can_cancel::boolean as can_cancel
        ,delivery_status:status::string as status
        ,delivery_status:emails_sent::int as emails_sent
        ,delivery_status:emails_canceled::int as emails_canceled
    from stg_mailchimp__campaigns
)

select * from int_mailchimp__campaign_delivery_status