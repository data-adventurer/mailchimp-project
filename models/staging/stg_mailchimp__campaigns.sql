with source_mailchimp_bronze as (

    select * from {{ source('mailchimp_raw', 'mailchimp_bronze') }}
  
),
stg_mailchimp__campaigns as (
    select
        json_data:id::string AS id
        ,json_data:web_id::int AS web_id
        ,json_data:type::string AS type
        ,json_data:create_time::timestamp AS create_time
        ,json_data:archive_url::string AS archive_url
        ,json_data:long_archive_url::string AS long_archive_url
        ,json_data:status::string AS status
        ,json_data:emails_sent::int AS emails_sent
        ,json_data:send_time::timestamp AS send_time
        ,json_data:content_type::string AS content_type
        ,json_data:needs_block_refresh::boolean AS needs_block_refresh
        ,json_data:resendable::boolean AS resendable
        ,json_data:recipients::variant AS recipients
        ,json_data:settings::variant AS settings
        ,json_data:tracking::variant AS tracking
        ,json_data:report_summary::variant AS report_summary
        ,json_data:delivery_status::variant AS delivery_status
    from source_mailchimp_bronze
)

select * from stg_mailchimp__campaigns