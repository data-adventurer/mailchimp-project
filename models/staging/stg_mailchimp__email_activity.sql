with source_mailchimp_bronze_email_activity as (

    select * from {{ source('mailchimp_raw', 'mailchimp_bronze_email_activity') }}
  
),
stg_mailchimp__email_activity as (

    select

        json_data:_airbyte_data:action::string as action
        ,json_data:_airbyte_data:campaign_id::string as campaign_id
        ,json_data:_airbyte_data:email_address::string as email_address
        ,json_data:_airbyte_data:email_id::string as email_id
        ,json_data:_airbyte_data:ip::string as ip
        ,json_data:_airbyte_data:list_id::string as list_id
        ,json_data:_airbyte_data:list_is_active::boolean as list_is_active
        ,try_to_timestamp_ntz(json_data:_airbyte_data:timestamp::string) as timestamp
        ,try_to_timestamp_ntz(json_data:_airbyte_extracted_at::string) as airbyte_extracted_at
        ,json_data:_airbyte_generation_id::int as airbyte_generation_id
        ,json_data:_airbyte_meta:sync_id::string as airbyte_sync_id
        ,json_data:_airbyte_raw_id::string as airbyte_raw_id

    from source_mailchimp_bronze_email_activity

)

select * from stg_mailchimp__email_activity