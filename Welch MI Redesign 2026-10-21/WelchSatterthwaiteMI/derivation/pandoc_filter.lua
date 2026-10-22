local title_removed = false

function Header(element)
  if not title_removed and element.level == 1 then
    title_removed = true
    return {}
  end

  if element.level > 1 then
    element.level = element.level - 1
  end
  return element
end

function Math(element)
  if element.mathtype == "DisplayMath" then
    local content = element.text:gsub("^%s+", ""):gsub("%s+$", "")
    return pandoc.RawInline(
      "latex",
      "\\begin{equation}\n" .. content .. "\n\\end{equation}"
    )
  end
  return element
end
