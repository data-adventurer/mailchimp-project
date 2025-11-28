    select distinct

        id as campaign_id
        ,settings:title::string as title
        ,settings:subject_line::string as subject_line
        
    from {{ ref('stg_mailchimp__campaigns') }}