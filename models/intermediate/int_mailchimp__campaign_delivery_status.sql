with base as (
    select
        id as campaign_id,
        delivery_status
    from {{ ref('stg_mailchimp__campaigns') }}
),

flattened as (
    select
        campaign_id,
        delivery_status:can_cancel::boolean as can_cancel,
        delivery_status:status::string as status,
        value:reason::string as reason
    from base,
    lateral flatten(input => delivery_status:reasons)
)

select * from flattened
