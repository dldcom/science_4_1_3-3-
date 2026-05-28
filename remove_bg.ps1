Add-Type -AssemblyName System.Drawing
$inFile = "C:\Users\dldco\.gemini\antigravity\brain\c5ee8fed-231c-4f7e-b767-f164954dbbc0\basalt_wall_front_1779974772196.png"
$outFile = "c:\Users\dldco\Downloads\claude\science_3\science_4_1_3-3-\wall_processed.png"
$bmp = New-Object System.Drawing.Bitmap($inFile)
$width = $bmp.Width
$height = $bmp.Height
for ($y = 0; $y -lt $height; $y++) {
    for ($x = 0; $x -lt $width; $x++) {
        $p = $bmp.GetPixel($x, $y)
        if ($p.R -gt 240 -and $p.G -gt 240 -and $p.B -gt 240) {
            $bmp.SetPixel($x, $y, [System.Drawing.Color]::Transparent)
        }
    }
}
$bmp.Save($outFile, [System.Drawing.Imaging.ImageFormat]::Png)
$bmp.Dispose()
