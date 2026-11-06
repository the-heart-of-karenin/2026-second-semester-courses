$ErrorActionPreference = 'Stop'
$faustRoot = Split-Path -Parent $PSScriptRoot
$faustDocx = Join-Path $faustRoot '浮士德 第一部与第二部 中文初译.docx'
$faustPdf = Join-Path $PSScriptRoot 'render\word_preview.pdf'
New-Item -ItemType Directory -Path (Split-Path -Parent $faustPdf) -Force | Out-Null
$faustWord = $null
$faustDocument = $null
try {
    $faustWord = New-Object -ComObject Word.Application
    $faustWord.Visible = $false
    $faustWord.DisplayAlerts = 0
    $faustWord.AutomationSecurity = 3
    $faustDocument = $faustWord.Documents.Open($faustDocx, $false, $true, $false)
    $faustDocument.Repaginate()
    $faustPages = $faustDocument.ComputeStatistics(2)
    $faustDocument.ExportAsFixedFormat($faustPdf, 17)
    Write-Output "Word pages: $faustPages"
    Write-Output "Preview: $faustPdf"
} finally {
    if ($null -ne $faustDocument) { $faustDocument.Close(0) }
    if ($null -ne $faustWord) { $faustWord.Quit(0) }
}
