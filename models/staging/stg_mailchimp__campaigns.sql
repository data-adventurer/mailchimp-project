with source_mailchimp_bronze_campaigns as (

    select * from {{ source('mailchimp_raw', 'mailchimp_bronze_campaigns') }}
  
),
stg_mailchimp__campaigns as (

    select

        json_data:_airbyte_data.id::string as id
        ,json_data:_airbyte_data.web_id::int as web_id
        ,json_data:_airbyte_data.type::string as type
        ,try_to_timestamp_ntz(json_data:_airbyte_data.create_time::string) as create_time
        ,json_data:_airbyte_data.archive_url::string as archive_url
        ,json_data:_airbyte_data.long_archive_url::string as long_archive_url
        ,json_data:_airbyte_data.status::string as status
        ,json_data:_airbyte_data.emails_sent::int as emails_sent
        ,try_to_timestamp_ntz(json_data:_airbyte_data.send_time::string) as send_time
        ,json_data:_airbyte_data.content_type::string as content_type
        ,json_data:_airbyte_data.needs_block_refresh::boolean as needs_block_refresh
        ,json_data:_airbyte_data.resendable::boolean as resendable
        ,json_data:_airbyte_data.recipients::variant as recipients
        ,json_data:_airbyte_data.settings::variant as settings
        ,json_data:_airbyte_data.tracking::variant as tracking
        ,json_data:_airbyte_data.report_summary::variant as report_summary
        ,json_data:_airbyte_data.delivery_status::variant as delivery_status
        ,try_to_timestamp_ntz(json_data:_airbyte_extracted_at::string) as airbyte_extracted_at

    from source_mailchimp_bronze_campaigns

)

select * from stg_mailchimp__campaigns