with stg_mailchimp__campaigns as (

    select * from {{ ref('stg_mailchimp__campaigns') }}
  
),
int_mailchimp__campaign_recipients as (

    select

        id as campaign_id,
        recipients:list_id::string as list_id,
        recipients:segment_text::string as segment_text,
        recipients:recipient_count::int as recipient_count

    from stg_mailchimp__campaigns
)

select * from int_mailchimp__campaign_recipients