#! /usr/bin/env fish

echo "Length of token:" (string length -- $TOKEN)
echo "Length of username:" (string length -- $USERNAME)

# All
set page 1
set all_repos

while true
    set repos (curl -sL \
	    -H "Authorization: Bearer $TOKEN"\
	    "https://api.github.com/user/repos?per_page=100&visibility=all&page=$page" \
	    | jq -r '.[] | select (.fork == false) | .full_name')
    
    if test (count $repos) -eq 0
        break
    end

    set all_repos $all_repos $repos
    set page (math $page + 1)
end

mkdir temp
cd temp

echo $TOKEN | gh auth login --with-token
for repo in $all_repos
  if not test (echo $repo | grep nvimdev)
    gh repo clone $repo -- --quiet > /dev/null 2>&1
  end
end
tokei -o json > ../stats_total.json

echo (count $all_repos) repos queried
