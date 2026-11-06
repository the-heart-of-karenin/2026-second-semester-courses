$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null=[Windows.Storage.StorageFile,Windows.Storage,ContentType=WindowsRuntime]
$null=[Windows.Graphics.Imaging.BitmapDecoder,Windows.Foundation,ContentType=WindowsRuntime]
$null=[Windows.Media.Ocr.OcrEngine,Windows.Foundation,ContentType=WindowsRuntime]
$asTask=([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object {$_.Name -eq 'AsTask' -and $_.IsGenericMethodDefinition -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1'})[0]
function Await($operation,$type) { $task=$asTask.MakeGenericMethod($type).Invoke($null,@($operation)); $task.Wait(); return $task.Result }
$null=[Windows.Globalization.Language,Windows.Foundation,ContentType=WindowsRuntime]
$lang=New-Object Windows.Globalization.Language 'zh-Hans-CN'
$engine=[Windows.Media.Ocr.OcrEngine]::TryCreateFromLanguage($lang)
$folder=Join-Path $PSScriptRoot '提取文本\Ahlfors_OCR'
foreach($p in Get-ChildItem -LiteralPath $folder -Filter '*.png' | Sort-Object Name) {
 $dest=[IO.Path]::ChangeExtension($p.FullName,'.txt')
 if(Test-Path -LiteralPath $dest){continue}
 $file=Await ([Windows.Storage.StorageFile]::GetFileFromPathAsync($p.FullName)) ([Windows.Storage.StorageFile])
 $stream=Await ($file.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
 $decoder=Await ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
 $bitmap=Await ($decoder.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
 $result=Await ($engine.RecognizeAsync($bitmap)) ([Windows.Media.Ocr.OcrResult])
 ($result.Lines | ForEach-Object {$_.Text}) | Set-Content -LiteralPath $dest -Encoding UTF8
 $bitmap.Dispose();$stream.Dispose()
 Write-Output $p.BaseName
}
