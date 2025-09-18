CREATE OR REPLACE VIEW lists_index AS
  SELECT topics.id as topic_id, topics.title, topics.category, lists.id, lists.author_id,
  json_agg(
    json_build_object(
      'rank', items.rank,
      'ext_id', items.external_id,
      'notes', items.notes
      )
    ) as items 
  FROM lists 
  INNER JOIN users on lists.author_id = users.id
  INNER JOIN topics on lists.topic_id = topics.id
  LEFT JOIN list_items items on items.list_id = lists.id
  GROUP BY topics.id, topics.title, topics.category, lists.id, lists.author_id;