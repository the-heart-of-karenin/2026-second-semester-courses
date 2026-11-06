$ErrorActionPreference = 'Stop'
$taskRoot = Split-Path -Parent $PSScriptRoot
$qaDir = Join-Path $PSScriptRoot 'qa_round8'
New-Item -ItemType Directory -Path $qaDir -Force | Out-Null
$manifest = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'manifest.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$word = $null; $doc = $null
try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false; $word.DisplayAlerts = 0
    $doc = $word.Documents.Open((Join-Path $taskRoot $manifest.books[1].working_docx),$false,$true)
    $doc.Repaginate()
    $doc.ExportAsFixedFormat((Join-Path $qaDir 'book2.pdf'),17)
    Write-Output "Book 2: $($doc.ComputeStatistics(2)) pages"
} finally {
    if ($null -ne $doc) { $doc.Close(0); [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($doc) }
    if ($null -ne $word) { $word.Quit(); [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) }
}
