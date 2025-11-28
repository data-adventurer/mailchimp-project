with ranked_activity as (
    select *,
        row_number() over (
            partition by email_address
            order by timestamp desc nulls last
        ) as row_num
    from {{ ref('stg_mailchimp__email_activity') }} 
), 
mailchimp__dim_emails as (
    select
        email_address
        ,ip
        ,email_id
        ,timestamp
    from ranked_activity
    where row_num = 1
)

select * from mailchimp__dim_emails