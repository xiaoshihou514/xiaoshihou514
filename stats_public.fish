#! /usr/bin/env fish

echo "Length of username:" (string length -- $USERNAME)

# All
set page 1
set all_repos

while true
    set repos (curl -sL \
	    "https://api.github.com/search/repositories?q=user:$USERNAME&per_page=100&page=$page" \
	    | jq -r '.items.[] | select (.fork == false) | .full_name')

    if test (count $repos) -eq 0
        break
    end

    set all_repos $all_repos $repos
    set page (math $page + 1)
end

cd temp

set filtered
for repo in $all_repos
    if not test (echo $repo | grep nvimdev)
        set repo_name (string split '/' $repo)[-1]
        set filtered $filtered $repo_name
    end
end
tokei -o json $filtered >../stats_public.json

echo (count $all_repos) repos queried
