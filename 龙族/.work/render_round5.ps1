$ErrorActionPreference = 'Stop'
$taskRoot = Split-Path -Parent $PSScriptRoot
$qaDir = Join-Path $PSScriptRoot 'qa_round5'
New-Item -ItemType Directory -Path $qaDir -Force | Out-Null
$manifest = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'manifest.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$word = $null
try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0
    foreach ($index in 0,1) {
        $doc = $null
        try {
            $docPath = Join-Path $taskRoot $manifest.books[$index].working_docx
            $pdfPath = Join-Path $qaDir ('book' + ($index+1) + '.pdf')
            $doc = $word.Documents.Open($docPath,$false,$true)
            $doc.Repaginate()
            $doc.ExportAsFixedFormat($pdfPath,17)
            Write-Output "Book $($index+1): $($doc.ComputeStatistics(2)) pages"
        } finally {
            if ($null -ne $doc) { $doc.Close(0); [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($doc) }
        }
    }
} finally {
    if ($null -ne $word) { $word.Quit(); [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) }
}
